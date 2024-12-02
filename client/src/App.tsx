import React, { useEffect, useState } from "react";
import AppRouter from "./config/navigation";
import { chechUserId, getCurrencies } from "./helpers";
import { useAppDispatch, useAppSelector } from "./store/hooks";
import { dispatchCurrencies } from "./store/slices/exchange";

const App = () => {
  const dispatch = useAppDispatch();
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    const loadAppData = async () => {
      chechUserId(); // Ensure this works correctly even if asynchronous

      try {
        const res = await getCurrencies();
        if (res) {
          dispatch(dispatchCurrencies(res));
        }
      } catch (error) {
        console.error("Error loading currencies:", error);
      } finally {
        setLoading(false); // Stop the loader once data is loaded
      }
    };

    loadAppData();
  }, [dispatch]);
  return (
    <div className="wrapper">
      {loading ? (
        <div className="preloader">
          <div className="preloader__circle"></div>
          <h3 className="preload__text">Loading coins, please wait</h3>
        </div>
      ) : (
        <AppRouter />
      )}
    </div>
  );
};

export default App;
