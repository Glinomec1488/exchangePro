import { useAppSelector } from "../../../../../../store/hooks";
import useCurrency from "../../hooks/useCurrency";
import { getActiveCurrencyStyle } from "./helpers";
interface IProps {
  isTo: boolean;
}

const CurrenciesList = ({ isTo }: IProps) => {
  const { setFromCurrency, setToCurrency } = useCurrency();
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
    <>
      {currencies
        ? currencies.map((currency) => (
            <li
              key={currency.fullName}
              className={`exchange__block-item exchange__block-item-send ${getActiveCurrencyStyle(
                isTo,
                currency.fullName,
                fromCurrency.fullName,
                toCurrency.fullName
              )}`}
              onClick={() => {
                handleSelectCurrency(currency.shortName, currency.fullName);
              }}
            >
              <img
                src={require(`../../../../../../static/${currency.imageUrlP}.svg`)} //{`${getEnv(process.env.REACT_APP_SERVER_URL,"REACT_APP_SERVER_URL")}/static/${currency.imageUrlP}.svg`}
                alt=""
              />
            </li>
          ))
        : ""}
    </>
  );
};

export default CurrenciesList;
