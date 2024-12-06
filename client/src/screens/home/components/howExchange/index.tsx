import steps from "../../../../assets/stepsnew.png";
import steps2 from "../../../../assets/steps2new.png";
import img from "../../../../assets/1new.png";
import img2 from "../../../../assets/2new.png";
import { AnimationOnScroll } from "react-animation-on-scroll";
import WalletBonus from "./components/walletBonus";

const HowExchange = () => {
  return (
    <section className="how-exchange" id="how-exchange">
      <div className="container how-exchange__container">
        <div className="how-exchange__wrapper">
          <AnimationOnScroll animateOnce animateIn="animate__fadeInLeft">
            <div className="how-exchange__start">
              <div className="how-exchange__text">
                HOW TO EXCHANGE YOUR CRYPTO?
              </div>
              <h3 className="title how-exchange__title">
                FOLLOW THESE SIMPLE STEPS:
              </h3>
              <img className="how-exchange__steps" src={steps} alt="steps" />
            </div>
          </AnimationOnScroll>
          <AnimationOnScroll animateOnce animateIn="animate__fadeInRight">
            <div className="how-exchange__end">
              <img className="how-exchange__steps-2" src={steps2} alt="steps" />
            </div>
          </AnimationOnScroll>
        </div>
        <AnimationOnScroll animateOnce animateIn="animate__fadeInUp">
          <div className="how-exchange__blocks">
            <WalletBonus />
            <div className="how-exchange__block">
              <div className="how-exchange__block-step">Step #2</div>
              <h4 className="how-exchange__block-title">
                Choose the coins pair
              </h4>
              <div className="how-exchange__block-text">
                For example Fatnom --&gt; Avalanche.
              </div>
              <img src={img} alt="" />
            </div>
            <div className="how-exchange__block">
              <div className="how-exchange__block-step">Step #3</div>
              <h4 className="how-exchange__block-title">
                Pay the request after filling the information fields
              </h4>
              <div className="how-exchange__block-text">
                After that — wait for the confirmation!
              </div>
              <img className="how-exchange__block-img" src={img2} alt="" />
            </div>
          </div>
        </AnimationOnScroll>
      </div>
    </section>
  );
};

export default HowExchange;
