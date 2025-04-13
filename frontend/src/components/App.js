import { useState, useEffect } from "react";
import { API_BASE_URL } from "../config";
import Blockchain from "./Blockchain";
import ConductTransaction from "./ConductTransaction";

function App() {
  const [walletInfo, setWalletInfo] = useState({});
  useEffect(() => {
    fetch(`${API_BASE_URL}/wallet/info`)
      .then((response) => response.json())
      .then((json) => {
        setWalletInfo(json);
      });
  }, []);

  const { address, balance } = walletInfo;

  return (
    <div className="App">
      <h3>Welcome to pychain</h3>
      <br />
      <div className="WalletInfo">
        <div>Address: {address}</div>
        <div>Balance: {balance}</div>
      </div>
      <br />
      <Blockchain />
      <br />
      <ConductTransaction />
    </div>
  );
}

export default App;
