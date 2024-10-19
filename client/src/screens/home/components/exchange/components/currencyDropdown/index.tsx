import { useState } from "react";
import "./styles.css";
import arrow from "../../../../../../assets/drop_arrow.svg";
import { getActiveCurrencyStyle } from "../currenciesList/helpers";
import { useAppSelector } from "../../../../../../store/hooks";
import { getEnv } from "../../../../../../utils";
import useCurrency from "../../hooks/useCurrency";

interface IProps {
  isTo: boolean;
}

const CurrencyDropDown = ({ isTo }: IProps) => {
  const [isActive, setIsActive] = useState(false);

  const {
    // currencies,
    setFromCurrency,
    setToCurrency,
  } = useCurrency();

  const toCurrency = useAppSelector((state) => state.exchange.toCurrency);
  const fromCurrency = useAppSelector((state) => state.exchange.fromCurrency);
  const currencies = useAppSelector((state) => state.exchange.currencies);

  const handleSelectCurrency = (shortName: string, fullName: string) => {
    if (isTo && fromCurrency.fullName !== fullName) {
      setToCurrency(shortName, fullName);
    }
    if (!isTo && toCurrency.fullName !== fullName) {
      setFromCurrency(shortName, fullName);
    }
  };

  return (
    <div className="drop_container">
      <div
        onClick={() => setIsActive((prev) => !prev)}
        className="exchange__block-title"
      >
        YOU SEND
        <img src={arrow} alt="" />
      </div>
      <div className={isActive ? "dropdown dropdown_active" : "dropdown"}>
        {currencies &&
          currencies.map((currency) => (
            <div
              key={currency.fullName}
              onClick={() =>
                handleSelectCurrency(currency.shortName, currency.fullName)
              }
              className={`exchange__block-item exchange__block-item-send ${getActiveCurrencyStyle(
                isTo,
                currency.fullName,
                fromCurrency.fullName,
                toCurrency.fullName
              )}`}
            >
              <img
                src={`${getEnv(
                  process.env.REACT_APP_SERVER_URL,
                  "REACT_APP_SERVER_URL"
                )}/static/${currency.imageUrlP}.svg`}
                alt=""
              />
            </div>
          ))}
      </div>
    </div>
  );
};

export default CurrencyDropDown;
