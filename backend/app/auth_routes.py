from datetime import datetime, timezone
from fastapi import APIRouter, Depends, Header, HTTPException, Response, Cookie
from sqlalchemy.orm import Session
from app.database import get_db
from app import db_models
from app.auth import verify_password, hash_password, create_access_token, create_refresh_token, decode_token, get_user_from_access_token, REFRESH_TTL_DAYS

router = APIRouter(prefix='/api/auth', tags=['Authentication'])
REFRESH_COOKIE = 'voxminds_refresh'


def user_view(u):
    return {'id': u.id, 'name': u.name, 'email': u.email, 'role': u.role, 'beneficiary_id': u.beneficiary_id}


def current_user(authorization: str | None, db: Session):
    if not authorization or not authorization.lower().startswith('bearer '):
        raise HTTPException(401, 'Authentication required')
    u = get_user_from_access_token(authorization.split(' ', 1)[1].strip(), db)
    if not u or not u.active:
        raise HTTPException(401, 'Access token expired or invalid')
    return u


def issue_tokens(response: Response, user, db: Session):
    access = create_access_token(user.id)
    refresh, jti, expires = create_refresh_token(user.id)
    db.add(db_models.RefreshSession(jti=jti, user_id=user.id, expires_at=expires))
    db.commit()
    response.set_cookie(REFRESH_COOKIE, refresh, httponly=True, secure=False, samesite='lax', max_age=REFRESH_TTL_DAYS * 86400, path='/api/auth')
    return {'success': True, 'access_token': access, 'token_type': 'bearer', 'expires_in': 15 * 60, 'user': user_view(user)}


@router.post('/login')
def login(data: dict, response: Response, db: Session = Depends(get_db)):
    email = (data.get('email') or '').strip().lower(); password = data.get('password') or ''
    u = db.query(db_models.User).filter(db_models.User.email == email).first()
    if not u or not verify_password(password, u.password_hash) or not u.active:
        raise HTTPException(401, 'Invalid email or password')
    return issue_tokens(response, u, db)


@router.post('/register')
def register(data: dict, response: Response, db: Session = Depends(get_db)):
    name = (data.get('name') or '').strip(); email = (data.get('email') or '').strip().lower(); password = data.get('password') or ''
    if len(name) < 2: raise HTTPException(422, 'Please enter your full name')
    if len(password) < 8: raise HTTPException(422, 'Password must be at least 8 characters')
    if '@' not in email: raise HTTPException(422, 'Enter a valid email address')
    if db.query(db_models.User).filter(db_models.User.email == email).first(): raise HTTPException(409, 'An account with this email already exists')
    b = db_models.Beneficiary(name=name, age=data.get('age'), language=data.get('language','en'), education=data.get('education'), current_livelihood=data.get('current_livelihood'), employment_preference=data.get('employment_preference','wage'), district=data.get('district'), state=data.get('state'), skills='', interests='', mobility_constraints='', family_occupation='', experience_years=0)
    db.add(b); db.flush()
    u = db_models.User(name=name, email=email, password_hash=hash_password(password), role='beneficiary', beneficiary_id=b.id, active=True)
    db.add(u); db.commit(); db.refresh(u)
    return issue_tokens(response, u, db)


@router.post('/refresh')
def refresh(response: Response, refresh_token: str | None = Cookie(default=None, alias=REFRESH_COOKIE), db: Session = Depends(get_db)):
    if not refresh_token: raise HTTPException(401, 'Refresh session required')
    payload = decode_token(refresh_token, 'refresh')
    if not payload: raise HTTPException(401, 'Refresh session expired or invalid')
    session = db.query(db_models.RefreshSession).filter(db_models.RefreshSession.jti == payload.get('jti')).first()
    if not session or session.revoked_at or session.expires_at < datetime.utcnow(): raise HTTPException(401, 'Refresh session revoked or expired')
    u = db.get(db_models.User, int(payload['sub']))
    if not u or not u.active: raise HTTPException(401, 'Account is inactive')
    session.revoked_at = datetime.utcnow()
    return issue_tokens(response, u, db)


@router.post('/logout')
def logout(response: Response, refresh_token: str | None = Cookie(default=None, alias=REFRESH_COOKIE), db: Session = Depends(get_db)):
    if refresh_token:
        payload = decode_token(refresh_token, 'refresh')
        if payload and payload.get('jti'):
            session = db.query(db_models.RefreshSession).filter(db_models.RefreshSession.jti == payload['jti']).first()
            if session and not session.revoked_at: session.revoked_at = datetime.utcnow(); db.commit()
    response.delete_cookie(REFRESH_COOKIE, path='/api/auth')
    return {'success': True, 'message': 'Signed out successfully'}


@router.get('/me')
def me(authorization: str | None = Header(default=None), db: Session = Depends(get_db)):
    return {'success': True, 'user': user_view(current_user(authorization, db))}
