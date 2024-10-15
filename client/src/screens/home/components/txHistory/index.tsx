import { AnimationOnScroll } from "react-animation-on-scroll"
import useHistory, { IHistoryItem } from "./useHistory"

const TxHistory = () => {
    const {
        history
    } = useHistory()

    return (
        <AnimationOnScroll animateOnce animateIn="animate__fadeInUp">
            <section className="transactions" id="transactions">
                <div className="container transactions__container">
                    <h3 className="transactions__title">
                        Live transactions
                        <div className="transactions__title-circle">
                            <span></span>
                        </div>
                    </h3>
                    <div className="transactions__table-wrapper">
                        <table className="transactions__table">
                            <tbody>
                                <tr className="transactions__tr-header">
                                    <th className="transactions__th">TxHash</th>
                                    <th className="transactions__th">Block</th>
                                    <th className="transactions__th">From</th>
                                    <th className="transactions__th">To</th>
                                    <th className="transactions__th">Value</th>
                                    <th className="transactions__th">Age</th>
                                </tr>
                                {
                                    history.map((elem, index) => {
                                        if (index === 0) return (
                                            <tr key={elem.txHash} className="transactions__tr animate__animated animate__fadeIn">
                                                {Object.keys(elem).map(key => (
                                                    <td className="transactions__td" key={key}>{elem[key as keyof IHistoryItem]}</td>
                                                ))}
                                                <td className="transactions__td transactions__td_blue">Right now</td>
                                            </tr>
                                        )

                                        return (
                                            <tr key={elem.txHash} className="transactions__tr">
                                                {Object.keys(elem).map(key => (
                                                    <td className="transactions__td" key={key}>{elem[key as keyof IHistoryItem]}</td>
                                                ))}
                                                <td className="transactions__td transactions__td_blue">Right now</td>
                                            </tr>
                                        )
                                    })
                                }
                                <tr className="transactions__tr">
                                    <td className="transactions__td">x3dtmhwnddf...</td>
                                    <td className="transactions__td">588726</td>
                                    <td className="transactions__td">72KS9B...</td>
                                    <td className="transactions__td">8F3076...</td>
                                    <td className="transactions__td">8.43 LTC</td>
                                    <td className="transactions__td transactions__td_blue">Right now</td>
                                </tr>
                                {/* <tr className="transactions__tr">
                                    <td className="transactions__td">8ifg8ctwpa8...</td>
                                    <td className="transactions__td">774269</td>
                                    <td className="transactions__td">A7E61J...</td>
                                    <td className="transactions__td">F45BB8...</td>
                                    <td className="transactions__td">963.13 NANO</td>
                                    <td className="transactions__td transactions__td_blue">Right now</td>
                                </tr>
                                <tr className="transactions__tr">
                                    <td className="transactions__td">cmla53spvik...</td>
                                    <td className="transactions__td">774009</td>
                                    <td className="transactions__td">984J8F...</td>
                                    <td className="transactions__td">065S22...</td>
                                    <td className="transactions__td">0.04 BTC</td>
                                    <td className="transactions__td transactions__td_blue">Right now</td>
                                </tr>
                                <tr className="transactions__tr">
                                    <td className="transactions__td">hkvqxdxvybs...</td>
                                    <td className="transactions__td">553990</td>
                                    <td className="transactions__td">S5K653...</td>
                                    <td className="transactions__td">6090KJ...</td>
                                    <td className="transactions__td">1824.46 XRP</td>
                                    <td className="transactions__td transactions__td_blue">Right now</td>
                                </tr>
                                <tr className="transactions__tr">
                                    <td className="transactions__td">110lnzd9imbe...</td>
                                    <td className="transactions__td">353175</td>
                                    <td className="transactions__td">FKK6FE...</td>
                                    <td className="transactions__td">8T6SFA...</td>
                                    <td className="transactions__td">10620.48 XLM</td>
                                    <td className="transactions__td transactions__td_blue">Right now</td>
                                </tr>

                                <tr className="transactions__tr">
                                    <td className="transactions__td">wgggoaslmqb...</td>
                                    <td className="transactions__td">372017</td>
                                    <td className="transactions__td">A35JJF...</td>
                                    <td className="transactions__td">38A0J0...</td>
                                    <td className="transactions__td">9835.35 TRX</td>
                                    <td className="transactions__td transactions__td_blue">Right now</td>
                                </tr>
                                <tr className="transactions__tr">
                                    <td className="transactions__td">un89zp6xqn...</td>
                                    <td className="transactions__td">156439</td>
                                    <td className="transactions__td">F0J0B4...</td>
                                    <td className="transactions__td">37F51B...</td>
                                    <td className="transactions__td">3063.48 FTM</td>
                                    <td className="transactions__td transactions__td_blue">Right now</td>
                                </tr>
                                <tr className="transactions__tr">
                                    <td className="transactions__td">t6z9t6otlb...</td>
                                    <td className="transactions__td">109767</td>
                                    <td className="transactions__td">JJ5T9J...</td>
                                    <td className="transactions__td">FJKT59...</td>
                                    <td className="transactions__td">0.49 ETH</td>
                                    <td className="transactions__td transactions__td_blue">Right now</td>
                                </tr> */}
                            </tbody>
                        </table>
                    </div>
                </div>
            </section>
        </AnimationOnScroll>
    )
}

export default TxHistory