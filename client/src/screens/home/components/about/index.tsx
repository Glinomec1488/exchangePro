import { useEffect } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import cryptoImg from "../../../../assets/ctypto.png";

const About = () => {
  const [URLSearchParams] = useSearchParams();
  const navigate = useNavigate();

  useEffect(() => {
    if (URLSearchParams.get("ref") !== null) {
      console.log("di");
      const prevRef = localStorage.getItem("ref");
      localStorage.setItem("ref", URLSearchParams.get("ref") || prevRef!);
      navigate("/");
    }
  });

  return (
    <section className="hero" id="about">
      <div className="container hero__container">
        <h1 className="title hero__title animate__animated animate__fadeInUp">
          New modern cryptocurrency exchange platform — <span>BestExc</span>
        </h1>
        <h2 className="subtitle hero__subtitle animate__animated animate__fadeInUp">
          We are happy to present you new biggest service to exchange your
          cryptocurrency. You can easily exchange every coin listed on Binance
          with lowest fee!
        </h2>
        <img
          className="hero__img animate__animated animate__fadeInUp"
          src={cryptoImg}
          alt="crypto"
        />
        <div className="hero__text animate__animated animate__fadeInUp">
          And many other coins are available!
        </div>
        <a
          className="header__btn animate__animated animate__fadeInUp"
          href="#exchange"
        >
          Exchange
        </a>
      </div>
    </section>
  );
};

export default About;
