import { createSlice, PayloadAction } from "@reduxjs/toolkit";
import { ICurrency } from "../../interfaces";

interface IInitialState {
  fromCurrency: {
    shortName: string;
    fullName: string;
  };
  toCurrency: {
    shortName: string;
    fullName: string;
  };
  captcha: {
    num1: string;
    num2: string;
    result: string;
    isValid: boolean;
  };

  receiver: string;
  isValidReceiver: boolean;
  email: string;
  referalCode: string;
  currencies: ICurrency[];
  orderInfo: {
    receiveAmount: string;
    receiveCurrency: string;
    sendAmount: string;
    sendCurrency: string;
    receiver: string;
    wallet: string;
    status: string;
  } | null;
}

const initialState: IInitialState = {
  fromCurrency: {
    shortName: "",
    fullName: "",
  },
  toCurrency: {
    shortName: "",
    fullName: "",
  },
  captcha: {
    num1: `${Math.floor(Math.random() * 20)}`,
    num2: `${Math.floor(Math.random() * 20)}`,
    result: "",
    isValid: true,
  },
  receiver: "",
  isValidReceiver: true,
  email: "",
  referalCode: "",
  currencies: [],
  orderInfo: null,
};

export const exchangeSile = createSlice({
  name: "exchange",
  initialState,
  reducers: {
    dispatchFromCurrency: (
      state,
      action: PayloadAction<IInitialState["fromCurrency"]>
    ) => {
      if (action.payload) {
        state.fromCurrency = action.payload;
      }
    },
    dispatchToCurrency: (
      state,
      action: PayloadAction<IInitialState["toCurrency"]>
    ) => {
      if (action.payload) {
        state.toCurrency = action.payload;
      }
    },
    generateCaptcha: (state) => {
      state.captcha.num1 = `${Math.floor(Math.random() * 20)}`;
      state.captcha.num2 = `${Math.floor(Math.random() * 20)}`;
    },
    dispatchCaptchaResult: (state, action: PayloadAction<string>) => {
      state.captcha.result = action.payload;
    },
    dispatchCaptchaIsValid: (state, action: PayloadAction<boolean>) => {
      state.captcha.isValid = action.payload;
    },
    dispatchReceiver: (state, action: PayloadAction<string>) => {
      state.receiver = action.payload;
    },
    dispatchIsValidReceiver: (state, action: PayloadAction<boolean>) => {
      state.isValidReceiver = action.payload;
    },
    dispatchEmail: (state, action: PayloadAction<string>) => {
      state.email = action.payload;
    },
    dispatchReferalCode: (state, action: PayloadAction<string>) => {
      state.referalCode = action.payload;
    },
    dispatchCurrencies: (state, action: PayloadAction<ICurrency[]>) => {
      state.currencies = action.payload;
      state.fromCurrency = action.payload[0];
      state.toCurrency = action.payload[12];
    },
    dispatchOrder: (
      state,
      action: PayloadAction<IInitialState["orderInfo"]>
    ) => {
      state.orderInfo = action.payload;
    },
  },
});

export const {
  dispatchFromCurrency,
  dispatchToCurrency,
  generateCaptcha,
  dispatchCaptchaResult,
  dispatchEmail,
  dispatchReceiver,
  dispatchIsValidReceiver,
  dispatchReferalCode,
  dispatchCaptchaIsValid,
  dispatchCurrencies,
  dispatchOrder,
} = exchangeSile.actions;
export default exchangeSile.reducer;
