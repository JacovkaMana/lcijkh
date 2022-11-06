import React, { useState } from "react";
import './App.css';
import HeaderBlock from './components/HeaderBlock/HeaderBlock';
import RequestContainer from './components/RequestContainer/RequestContainer';

function App() {

  const [currentPath, setCurrentPath] = useState('active');

  return (
    <div className='App'>

      <HeaderBlock
        currentPath={currentPath}
        setCurrentPath={setCurrentPath}
      />

      <RequestContainer
        currentPath={currentPath}
      />

    </div>
  );
}

export default App;
