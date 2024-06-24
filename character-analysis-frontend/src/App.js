import React, { useState } from 'react';

function App() {
  const [file, setFile] = useState(null);
  const [analysis, setAnalysis] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleSubmit = async () => {
    if (!file) return;

    const reader = new FileReader();
    reader.onload = async (event) => {
      const script = event.target.result;

      const response = await fetch('http://127.0.0.1:5000/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ script }),
      });

      const data = await response.json();
      setAnalysis(data);
    };

    reader.readAsText(file);
  };

  return (
    <div className="App">
      <h1>Character Analysis Tool</h1>
      <input type="file" onChange={handleFileChange} />
      <button onClick={handleSubmit}>Analyze</button>
      <div>
        {analysis &&
          Object.keys(analysis).map((character) => (
            <div key={character}>
              <h3>{character}</h3>
              <p>{analysis[character]}</p>
            </div>
          ))}
      </div>
    </div>
  );
}

export default App;
