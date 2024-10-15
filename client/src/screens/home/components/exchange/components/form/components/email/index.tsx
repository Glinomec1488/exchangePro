import { useAppDispatch, useAppSelector } from "../../../../../../../../store/hooks"
import { dispatchEmail } from "../../../../../../../../store/slices/exchange"

const Email = () => {
    const {
        email
    } = useAppSelector(state => state.exchange)
    const dispatch = useAppDispatch()

    return (
        <div className="exchange__block-wrapper">
            <div className="exchange__block-text">
                E-mail
            </div>
            <input
                className="exchange__block-input exchange__block-input-email"
                type="email"
                placeholder="E-mail"
                value={email}
                onChange={e => dispatch(dispatchEmail(e.target.value))}
                required />
        </div>
    )
}

export default Email