import { useState, useEffect } from "react";
import { FormGroup, FormControl, Button } from "react-bootstrap";
import { Link, useNavigate } from "react-router-dom";
import { API_BASE_URL } from "../config";

function ConductTransaction() {
  const [amount, setAmount] = useState(0);
  const [recipient, setRecipient] = useState("");
  const [knownAddresses, setKnownAddresses] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    fetch(`${API_BASE_URL}/known-addresses`)
      .then((r) => r.json())
      .then((json) => setKnownAddresses(json));
  }, []);

  const updateRecipient = (e) => {
    setRecipient(e.target.value);
  };

  const updateAmount = (e) => {
    setAmount(Number(e.target.value));
  };

  const submitTransaction = () => {
    fetch(`${API_BASE_URL}/wallet/transact`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ recipient, amount }),
    })
      .then((r) => r.json())
      .then((json) => {
        navigate("/transaction-pool");
      });
  };

  return (
    <div className="ConductTransaction">
      <Link to="/">Home</Link>
      <hr />
      <h3>Conduct a Transaction</h3>
      <br />
      <FormGroup>
        <FormControl
          input="text"
          placeholder="recipient"
          value={recipient}
          onChange={updateRecipient}
        />
      </FormGroup>

      <FormGroup>
        <FormControl
          input="number"
          placeholder="amount"
          value={amount}
          onChange={updateAmount}
        />
      </FormGroup>

      <div>
        <Button variant="danger" onClick={submitTransaction}>
          Submit
        </Button>
      </div>
      <br />
      <h4>Known Addresses</h4>
      <div>
        {knownAddresses.map((knownAddress, i) => (
          <span key={knownAddress}>
            <u>{knownAddress}</u>
            {i < knownAddresses.length && ", "}
          </span>
        ))}
      </div>
    </div>
  );
}

export default ConductTransaction;
