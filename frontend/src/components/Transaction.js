function Transaction({ transaction }) {
  const { input, output } = transaction;
  const recipients = Object.keys(output);
  return (
    <div className="transaction">
      <div>From: {input.address}</div>
      {recipients.map((recipient) => (
        <div key={recipient}>
          To: {recipient} | Sent: {output[recipient]}
        </div>
      ))}
    </div>
  );
}

export default Transaction;
