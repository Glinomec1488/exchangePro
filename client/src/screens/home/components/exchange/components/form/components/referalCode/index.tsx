import {
  useAppDispatch,
  useAppSelector,
} from "../../../../../../../../store/hooks";
import {
  dispatchEmail,
  dispatchReferalCode,
} from "../../../../../../../../store/slices/exchange";
import React, { useState, useEffect } from "react";

const ReferalCode: React.FC = () => {
  //const referalCode = localStorage.getItem("ref");
  //const getReferalCode = "";
  const [referalCode, setReferalCode] = useState("");

  // Load the initial referral code from localStorage
  useEffect(() => {
    const storedCode = localStorage.getItem("ref");
    if (storedCode) {
      setReferalCode(storedCode);
    }
  }, []);

  // Function to handle input changes
  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newCode = e.target.value;
    setReferalCode(newCode);
    localStorage.setItem("ref", newCode); // Update localStorage with the new referral code
  };
  return (
    <div className="exchange__block-wrapper">
      <div className="exchange__block-text">Referral code</div>
      <input
        className="exchange__block-input"
        type="text"
        placeholder="Referral code"
        value={referalCode || ""}
        onChange={handleInputChange}
      />
    </div>
  );
};

export default ReferalCode;
