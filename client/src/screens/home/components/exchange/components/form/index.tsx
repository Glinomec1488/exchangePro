import React, { useState, useEffect } from "react";
import { useAppSelector } from "../../../../../../store/hooks";
import useExchangeRate from "./hooks/useExchangeRate";
import Captcha from "./components/captcha";
import Email from "./components/email";
import Receiver from "./components/receiver";
import ReferalCode from "./components/referalCode";
import useForm from "./hooks/useForm";

let isLoaded: boolean = false;

export const setIsLoaded = (loaded: boolean) => {
  isLoaded = loaded;
};
export const getIsLoaded = (): boolean => {
  return isLoaded;
};

export const Form = () => {
  const { fromCurrency, toCurrency } = useAppSelector(
    (state) => state.exchange
  );

  const {
    exchangeRate,
    toCurrencyAmount,
    fromCurrencyAmount,
    setFromCurrencyAmount,
    setToCurrencyAmount,
    setIsChangeInput,
  } = useExchangeRate();

  const [tempAmount, setTempAmount] = useState<string>(fromCurrencyAmount);
  const [loading, setLoading] = useState<boolean>(true); // Loading state
  const [isValid, setIsValid] = useState<boolean>(true);

  const validateInput = (amount: string) => {
    const numericAmount = Number(amount);
    const isWithinRange =
      numericAmount >= exchangeRate.fromCurrenycRange.from &&
      numericAmount <= exchangeRate.fromCurrenycRange.to;

    setIsValid(isWithinRange); // Update isValid based on range check
    if (!getIsLoaded()) {
      setLoading(true);
    }
    if (isWithinRange) {
      setIsChangeInput(true);
      setFromCurrencyAmount(amount);
      if (getIsLoaded()) {
        setLoading(false);
      }
    } else {
      setIsLoaded(false);
    }
  };

  useEffect(() => {
    setLoading(true);
    validateInput(tempAmount);
  });

  const { sendForm } = useForm();

  return (
    <form
      onSubmit={async (e) =>
        await sendForm(e, fromCurrencyAmount, toCurrencyAmount)
      }
      className="exchange__block-form"
    >
      <div className="exchange__block-wrapper">
        <div className="exchange__block-text exchange__block-text-send">
          You send{" "}
          <span>
            ({exchangeRate.fromCurrenycRange.from} —{" "}
            {exchangeRate.fromCurrenycRange.to})
          </span>
        </div>
        <div className="exchange__block-header exchange__block-header-send">
          {fromCurrency.fullName}
        </div>
        <input
          className="exchange__block-input exchange__block-input-val exchange__block-input-send"
          type="number"
          step="any"
          value={tempAmount}
          onChange={(e) => {
            setTempAmount(e.target.value);
            validateInput(tempAmount);
          }}
        />
      </div>
      <div className="exchange__block-wrapper">
        <div className="exchange__block-text exchange__block-text-receive">
          You receive
        </div>
        <div className="exchange__block-header exchange__block-header-receive">
          {toCurrency.fullName}
        </div>
        <input
          className={`exchange__block-input exchange__block-input-val exchange__block-input-receive ${
            loading ? "loading" : ""
          }`}
          type="number"
          step="any"
          value={toCurrencyAmount}
          onChange={(e) => {
            setIsChangeInput(true);
            setToCurrencyAmount(e.target.value);
          }}
          readOnly
        />
      </div>
      <Receiver />
      <Email />
      <ReferalCode />
      <Captcha />
      <button className="exchange__block-btn" disabled={loading || !isValid}>
        Continue
      </button>
    </form>
  );
};

export default Form;
