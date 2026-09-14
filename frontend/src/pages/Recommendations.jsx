function Recommendations() {
  const recommendations = [
    {
      title: "Agricultural Equipment Technician",
      nsqfLevel: "NSQF Level 4",
      score: 92,
      reason:
        "Matches your farming experience and interest in machinery."
    },
    {
      title: "Tractor Operator",
      nsqfLevel: "NSQF Level 3",
      score: 86,
      reason:
        "Matches your existing agricultural machinery experience."
    },
    {
      title: "Solar PV Installer",
      nsqfLevel: "NSQF Level 4",
      score: 78,
      reason:
        "Suitable technical pathway with local employability potential."
    }
  ];

  return (
    <div>
      <h1>Recommended Career Paths</h1>

      {recommendations.map((item) => (
        <div key={item.title}>
          <h2>{item.title}</h2>

          <p>
            {item.nsqfLevel}
          </p>

          <p>
            Suitability Score: {item.score}%
          </p>

          <p>
            {item.reason}
          </p>

          <hr />
        </div>
      ))}
    </div>
  );
}

export default Recommendations;