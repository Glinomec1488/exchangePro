import { AnimationOnScroll } from "react-animation-on-scroll";
import CurrenciesList from "./components/currenciesList";
import CurrencyDropDown from "./components/currencyDropdown";
import Form from "./components/form";

const Exchange = () => {
  return (
    <section className="exchange" id="exchange">
      <div className="container exchange__container">
        <AnimationOnScroll animateOnce animateIn="animate__fadeInDown">
          <div className="exchange__text">
            START THE EXCHANGE IN JUST FEW CLICKS!
          </div>
        </AnimationOnScroll>
        <AnimationOnScroll
          animateOnce
          delay={250}
          animateIn="animate__fadeInDown"
        >
          <h3 className="title exchange__title">CHOOSE THE PAIR TO EXCHANGE</h3>
        </AnimationOnScroll>
        <AnimationOnScroll
          animateOnce
          delay={500}
          animateIn="animate__fadeInUp"
        >
          <div className="exchange__wrapper">
            <div className="exchange__block exchange__block_big">
              <CurrencyDropDown isTo={false} text="YOU SEND" />
              <div className="exchange__block-title  desktop">YOU SEND</div>
              <ul className="exchange__block-list exchange__block-list-send">
                <CurrenciesList isTo={false} />
              </ul>
            </div>
            <div className="exchange__block exchange__block_big">
              <CurrencyDropDown isTo={true} text="YOU RECEIVE" />
              <div className="exchange__block-title desktop">YOU RECEIVE</div>
              <ul className="exchange__block-list exchange__block-list-receive">
                <CurrenciesList isTo={true} />
              </ul>
            </div>
            <div className="exchange__block exchange__block_small">
              <div className="exchange__block-title">FILL THE FIELDS</div>
              <Form />
            </div>
          </div>
        </AnimationOnScroll>
      </div>
    </section>
  );
};

export default Exchange;
