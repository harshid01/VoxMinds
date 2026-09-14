function Roadmap() {
  const roadmap = [
    {
      step: 1,
      title: "Current Skills",
      description:
        "Farming, equipment operation and basic machinery knowledge."
    },
    {
      step: 2,
      title: "Skill Assessment",
      description:
        "Assess machinery maintenance, diagnostics and safety skills."
    },
    {
      step: 3,
      title: "Recommended Training",
      description:
        "Training aligned with the selected NSQF job role."
    },
    {
      step: 4,
      title: "Certification",
      description:
        "Complete training and obtain relevant certification."
    },
    {
      step: 5,
      title: "Livelihood",
      description:
        "Explore wage employment or self-employment opportunities."
    }
  ];

  return (
    <div>
      <h1>Your Livelihood Roadmap</h1>

      {roadmap.map((item) => (
        <div key={item.step}>
          <h2>
            Step {item.step}: {item.title}
          </h2>

          <p>
            {item.description}
          </p>

          <hr />
        </div>
      ))}
    </div>
  );
}

export default Roadmap;