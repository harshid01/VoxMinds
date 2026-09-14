function Profile() {
  const profile = {
    name: "Ravi",
    education: "10th",
    current_livelihood: "Agriculture",
    skills: [
      "Farming",
      "Basic machinery"
    ],
    interests: [
      "Mechanical work"
    ],
    employment_preference: "Wage Employment",
    district: "Ahmedabad"
  };

  return (
    <div>
      <h1>Your Profile</h1>

      <p>
        <strong>Name:</strong> {profile.name}
      </p>

      <p>
        <strong>Education:</strong> {profile.education}
      </p>

      <p>
        <strong>Current livelihood:</strong>{" "}
        {profile.current_livelihood}
      </p>

      <p>
        <strong>Skills:</strong>{" "}
        {profile.skills.join(", ")}
      </p>

      <p>
        <strong>Interests:</strong>{" "}
        {profile.interests.join(", ")}
      </p>

      <p>
        <strong>Preference:</strong>{" "}
        {profile.employment_preference}
      </p>

      <p>
        <strong>District:</strong>{" "}
        {profile.district}
      </p>
    </div>
  );
}

export default Profile;