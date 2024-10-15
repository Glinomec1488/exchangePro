import { useAppDispatch, useAppSelector } from "../../../../../../../../store/hooks"
import { dispatchReceiver } from "../../../../../../../../store/slices/exchange"

const Receiver = () => {
    const {
        receiver,
        isValidReceiver
    } = useAppSelector(state => state.exchange)
    const dispatch = useAppDispatch()

    return (
        <div className="exchange__block-wrapper">
            <div className="exchange__block-text">
                Receive address
            </div>
            <input
                className={
                    isValidReceiver
                        ? "exchange__block-input exchange__block-input-receive-address"
                        : "exchange__block-input exchange__block-input-receive-address exchange_wrong_captcha"
                }
                type="text"
                placeholder="Your address"
                value={receiver}
                onChange={e => dispatch(dispatchReceiver(e.target.value))}
                required />
        </div>
    )
}

export default Receiver