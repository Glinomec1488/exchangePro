import React, { useEffect } from 'react';
import AppRouter from './config/navigation';
import { chechUserId, getCurrencies } from './helpers';
import { useAppDispatch, useAppSelector } from './store/hooks';
import { dispatchCurrencies } from './store/slices/exchange';

const App = () => {
  const dispatch = useAppDispatch()

  useEffect(() => {
    chechUserId()
    getCurrencies().then(res => {
      if (res) {
        dispatch(dispatchCurrencies(res))
      }
    })
  })

  return (
    <div className="wrapper">
      {/* <div className="preloader">
        <div className="preloader__circle"></div>
      </div> */}
      <AppRouter />
    </div>
  )
}

export default App;
