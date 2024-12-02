import { useState, useRef } from "react";
import "./styles.css";
import arrow from "../../../../../../assets/drop_arrow.svg";
import { getActiveCurrencyStyle } from "../currenciesList/helpers";
import { useAppSelector } from "../../../../../../store/hooks";
import useCurrency from "../../hooks/useCurrency";
interface IProps {
  isTo: boolean;
  text: string;
}

const CurrencyDropDown = ({ isTo, text }: IProps) => {
  const [isActive, setIsActive] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);
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
  const toggleDropdown = () => {
    if (dropdownRef.current) {
      const element = dropdownRef.current;
      if (isActive) {
        // Collapse: Set height to 0
        element.style.maxHeight = "0px";
      } else {
        // Expand: Set height to the content's scrollHeight
        element.style.maxHeight = `${element.scrollHeight}px`;
      }

      setIsActive((prev) => !prev); // Toggle active state
    }
  };
  return (
    <div className="drop_container">
      <div
        onClick={toggleDropdown}
        ref={dropdownRef}
        className="exchange__block-title"
        style={{
          maxHeight: "0", // Start collapsed
          overflow: "visible", // Hide content outside bounds
          transition: "max-height 0.3s ease-in-out", // Smooth animation
        }}
      >
        {text}
        <img src={arrow} alt="" />
      </div>
      <div className={isActive ? "dropdown dropdown_active" : "dropdown"}>
        {currencies &&
          currencies.map((currency) => (
            <div
              key={currency.fullName}
              onClick={() => {
                handleSelectCurrency(currency.shortName, currency.fullName);
              }}
              className={`exchange__block-item exchange__block-item-send ${getActiveCurrencyStyle(
                isTo,
                currency.fullName,
                fromCurrency.fullName,
                toCurrency.fullName
              )}`}
            >
              <img
                src={require(`../../../../../../static/${currency.imageUrlP}.svg`)} //{`${getEnv(process.env.REACT_APP_SERVER_URL,"REACT_APP_SERVER_URL")}/static/${currency.imageUrlP}.svg`}
                alt=""
              />
            </div>
          ))}
      </div>
    </div>
  );
};

export default CurrencyDropDown;
