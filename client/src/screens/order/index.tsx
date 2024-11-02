import coinSvg from "../../assets/coin.svg";
import walletSvg from "../../assets/wallet.svg";
import QRCode from "react-qr-code";
import useOrderInfo from "../../hooks/useOrderInfo";
import { copyToClipboard, cutAddress } from "../../helpers";
import { Link } from "react-router-dom";

const Order = () => {
  const { orderInfo, orderId, confirmOrder } = useOrderInfo();

  return (
    <main className="main">
      <section className="transaction">
        <div className="container transaction__container animate__animated animate__fadeInUp">
          <h1 className="transaction__title">
            Exchange <br />
            {orderInfo?.sendCurrency} on {orderInfo?.receiveCurrency}
          </h1>
          <div className="transaction__order">
            Order ID <span>{orderId}</span>
          </div>

          {orderInfo?.status !== "passed" &&
            orderInfo?.status !== "confirmed" && (
              <div className="transaction-1">
                <div className="transaction__block">
                  <div className="transaction__block-title">
                    Pay directly to the wallet
                  </div>
                  <div className="transaction__block-wrapper">
                    <div className="transaction__block-text">
                      You send: {orderInfo?.sendAmount}{" "}
                      {orderInfo?.sendCurrency}
                    </div>
                    <div className="transaction__block-text">
                      You receive: {orderInfo?.receiveAmount}{" "}
                      {orderInfo?.receiveCurrency}
                    </div>
                  </div>
                  <div className="transaction__block-input-wrapper">
                    <div
                      className="transaction__block-input-img"
                      style={{ marginLeft: "-5%" }}
                    >
                      <img src={coinSvg} alt="coin" />
                    </div>
                    <input
                      className="transaction__block-input"
                      type="text"
                      value={`${orderInfo?.sendAmount} ${orderInfo?.sendCurrency}`}
                      readOnly
                    />
                    <div
                      className="transaction__block-input-copy transaction__block-input-copy-val"
                      onClick={() =>
                        copyToClipboard(
                          `${orderInfo?.sendAmount} ${orderInfo?.sendCurrency}`
                        )
                      }
                    >
                      Click to copy
                    </div>
                  </div>
                  <div className="transaction__block-input-wrapper">
                    <div
                      className="transaction__block-input-img"
                      style={{ marginLeft: "-5%" }}
                    >
                      <img src={walletSvg} alt="wallet" />
                    </div>
                    <input
                      className="transaction__block-input"
                      type="text"
                      value={cutAddress(orderInfo?.wallet || "")}
                      readOnly
                    />
                    <div
                      className="transaction__block-input-copy transaction__block-input-copy-wallet"
                      onClick={() => copyToClipboard(orderInfo?.wallet || "")}
                    >
                      Click to copy
                    </div>
                  </div>
                  <button
                    className="transaction__block-btn"
                    onClick={async () => await confirmOrder()}
                  >
                    <span>Confirm</span>
                  </button>
                </div>
                <div className="transaction__block">
                  <div className="transaction__block-title">
                    Pay by scanning the QR code!
                  </div>
                  <div className="transaction__block-qr">
                    <QRCode
                      //value="ethereum:0xb794f5ea0ba39494ce839613fffba74279579268?amount=2.34"
                      value={`${orderInfo?.sendCurrency}:${orderInfo?.wallet}?amount=${orderInfo?.sendAmount}`}
                      style={{
                        maxHeight: "170px",
                        backgroundColor: "#fff",
                        display: "flex",
                        alignItems: "center",
                        justifyContent: "center",
                        padding: "25px 0",
                        borderRadius: "15px",
                      }}
                    />
                  </div>
                </div>
              </div>
            )}
          {orderInfo?.status === "confirmed" && (
            <div className="transaction-4">
              <div className="transaction__status transaction__status_blue">
                WAITING FOR CONFIRMATIONS
              </div>
              <div className="transaction__status-text">
                We are waiting to receive at least one confirmation!
              </div>
              <div className="load">
                <div className="load-value"></div>
              </div>
            </div>
          )}
          {orderInfo?.status === "passed" && (
            <div className="transaction-3">
              <div className="transaction__status transaction__status_green">
                ORDER COMPLETED
              </div>
              <div className="transaction__status-text">
                Your order has been completed successfully!
              </div>
              {
                <div className="transaction__status-text">
                  the time of arrival of funds may vary
                </div>
              }
            </div>
          )}
          <div className="transaction__btns">
            <Link className="transaction__btn" to="/">
              Get back
            </Link>
          </div>
        </div>
      </section>
    </main>
  );
};

export default Order;
