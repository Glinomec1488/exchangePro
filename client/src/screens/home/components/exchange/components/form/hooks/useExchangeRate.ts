import { useEffect, useState } from "react";
import { serveUrl } from "../../../../../../../config";
import { useAppSelector } from "../../../../../../../store/hooks";
import { setIsLoaded } from "..";

const getFixedAmount = (amount: number) => {
  if (amount.toFixed(6) === "0,000000" || amount.toFixed(6) === "0.000000")
    return "0";
  return amount.toFixed(7);
};
const ranges: Record<string, { min: number; max: number }> = {
  BTC: { min: 0.0001, max: 100 },
  ETH: { min: 0.02, max: 1000 },
  BNB: { min: 0.08, max: 1000 },
  BCH: { min: 0.15, max: 1000 },
  ZEC: { min: 1, max: 1488 },
  FTM: { min: 74, max: 10090 },
  SOL: { min: 0.3, max: 1001 },
  LTC: { min: 0.77, max: 1021 },
  TRX: { min: 293, max: 1900530 },
  ZRX: { min: 157, max: 100063 },
  XRP: { min: 92, max: 10000 },
  USDT: { min: 44, max: 106051 },
  ADA: { min: 141, max: 100000 },
  XTZ: { min: 72, max: 100067 },
  XMR: { min: 0.3, max: 1055 },
  DASH: { min: 2.1, max: 10083 },
  DOGE: { min: 449, max: 1220000 },
  DOT: { min: 11, max: 100554 },
};

const filterShortName = (input: string) => {
  return input.replace(/\(.*?\)/g, "").trim();
};

const useExchangeRate = () => {
  const { fromCurrency, toCurrency } = useAppSelector(
    (state) => state.exchange
  );

  const [fromCurrencyAmount, setFromCurrencyAmount] = useState("1");
  const [toCurrencyAmount, setToCurrencyAmount] = useState("");
  const [isChangeInput, setIsChangeInput] = useState(true);
  const [isChangeToCurrency, setIsChangeToCurrency] = useState(false);
  const [isChangeFromCurrency, setIsChangeFromCurrency] = useState(false);
  const noNetShrtTo = filterShortName(fromCurrency.shortName);
  const noNetShrtFrom = filterShortName(toCurrency.shortName);
  const [minAmount, setMinAmount] = useState(1);
  const [maxAmount, setMaxAmount] = useState(1);

  const getExchangeRate = async (
    toCurrencyAmount: string,
    fromCurrencyAmount: string,
    isChangeReceiveAmount: boolean
  ) => {
    if (!isChangeInput || !toCurrency.shortName || !fromCurrency.shortName)
      return;
    const isChange = isChangeReceiveAmount ? "True" : "false";
    setIsLoaded(false);
    try {
      const newForm = await fetch(
        `${serveUrl}/calculator/${noNetShrtTo}/${noNetShrtFrom}/${
          fromCurrencyAmount || "0.01"
        }/${toCurrencyAmount || "0.01"}/${isChange}`,
        {
          method: "POST",
        }
      ).then((res) => res.json());

      /*if (isChangeReceiveAmount) {
        setFromCurrencyAmount(getFixedAmount(newForm.amount));
      } else {*/
      setToCurrencyAmount(getFixedAmount(newForm.amount));
      //}
      setIsChangeInput(false);
    } catch (error) {
      console.error("Error fetching data:", error);
      // Optionally handle any errors if needed
    }
    setIsLoaded(true);
  };

  const getFromCurrencyRange = (currency: string) => {
    return ranges[currency] || { min: "0", max: "0" }; // Default range if currency is not found
  };

  useEffect(() => {
    getExchangeRate(toCurrencyAmount, fromCurrencyAmount, false);
  }, [fromCurrencyAmount, isChangeFromCurrency]);

  useEffect(() => {
    getExchangeRate(toCurrencyAmount, fromCurrencyAmount, false);
  }, [toCurrencyAmount, isChangeToCurrency]);

  useEffect(() => {
    setIsChangeInput(true);
    setIsChangeFromCurrency((prev) => !prev);
  }, [fromCurrency]);

  useEffect(() => {
    setIsChangeInput(true);
    setIsChangeToCurrency((prev) => !prev);
  }, [toCurrency]);

  useEffect(() => {
    if (noNetShrtTo) {
      const range = getFromCurrencyRange(noNetShrtTo);
      setMinAmount(range.min);
      setMaxAmount(range.max);
    }
  }, [fromCurrency]);

  const config = {
    fromCurrenycRange: {
      from: minAmount,
      to: maxAmount,
    },
    toCurrenycRange: {
      from: 0,
      to: 0,
    },
  };

  const changeFromAmount = (amount: string) => {
    if (
      Number(amount) <= config.fromCurrenycRange.to &&
      Number(amount) >= config.fromCurrenycRange.from
    ) {
      setFromCurrencyAmount(amount);
    } else {
      setFromCurrencyAmount(`${config.fromCurrenycRange.from}`);
    }
  };

  const changeToAmount = (amount: string) => {
    if (
      Number(amount) <= config.toCurrenycRange.to &&
      Number(amount) >= config.toCurrenycRange.from
    ) {
      setToCurrencyAmount(amount);
    } else {
      setToCurrencyAmount(`${config.toCurrenycRange.from}`);
    }
  };
  return {
    exchangeRate: config,
    fromCurrencyAmount,
    toCurrencyAmount,
    setFromCurrencyAmount: changeFromAmount,
    setToCurrencyAmount: changeToAmount,
    setIsChangeInput,
  };
};

export default useExchangeRate;
