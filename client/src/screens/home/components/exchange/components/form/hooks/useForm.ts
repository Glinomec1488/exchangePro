import { useNavigate } from "react-router-dom";
import { serveUrl } from "../../../../../../../config";
import {
  useAppDispatch,
  useAppSelector,
} from "../../../../../../../store/hooks";
import {
  dispatchCaptchaIsValid,
  dispatchIsValidReceiver,
  dispatchOrder,
  generateCaptcha,
} from "../../../../../../../store/slices/exchange";

const useForm = () => {
  const { captcha, email, receiver, fromCurrency, toCurrency } = useAppSelector(
    (state) => state.exchange
  );

  const dispatch = useAppDispatch();
  const navigate = useNavigate();

  const validateCaptcha = () => {
    if (
      Number(captcha.num1) + Number(captcha.num2) ===
      Number(captcha.result)
    ) {
      dispatch(dispatchCaptchaIsValid(true));
      return true;
    }

    dispatch(dispatchCaptchaIsValid(false));
    dispatch(generateCaptcha());
    return false;
  };

  const validateReceiver = () => {
    const regex = /^[A-Za-z0-9]{5,100}$/; //^[A-Za-z0-9]{5,100}[0-9a-fA-F]+$/i; //^(0x){1}[0-9a-fA-F]{40}$/i;

    if (regex.test(receiver)) {
      dispatch(dispatchIsValidReceiver(true));
      return true;
    }

    dispatch(dispatchIsValidReceiver(false));
    return false;
  };

  const sendForm = async (
    e: React.FormEvent<HTMLFormElement>,
    sendAmount: string,
    receiveAmount: string
  ) => {
    try {
      e.preventDefault();

      const isValidCaptcha = validateCaptcha();
      const isValidReceiver = validateReceiver();

      if (!isValidCaptcha || !isValidReceiver) return null;

      const referalCode = localStorage.getItem("ref");

      const res = await fetch(
        `${serveUrl}/newOrder/${receiveAmount}/${
          toCurrency.shortName
        }/${sendAmount}/${fromCurrency.shortName}/${receiver}/${email}/${
          referalCode || "null"
        }/pending`,
        {
          method: "GET",
        }
      ).then((res) => res.json());

      if (res.orderId) {
        const order = await fetch(`${serveUrl}/order/${res.orderId}`).then(
          (res) => res.json()
        );

        dispatch(dispatchOrder(order));

        navigate(`/order/${res.orderId}`);
      } else {
        throw new Error("something went wrong with order id");
      }
    } catch (error: any) {
      console.error(error.message);
    }
  };

  return {
    sendForm,
  };
};

export default useForm;
