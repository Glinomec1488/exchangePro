import { useAppDispatch, useAppSelector } from "../../../../../../../../store/hooks"
import { dispatchEmail, dispatchReferalCode } from "../../../../../../../../store/slices/exchange"

const ReferalCode = () => {
    const referalCode = localStorage.getItem('ref')

    return (
        <div className="exchange__block-wrapper">
            <div className="exchange__block-text">
                Referral code
            </div>
            <input
                className="exchange__block-input"
                type="text"
                placeholder="Referral code"
                value={referalCode || ''}
                readOnly
            />
        </div>
    )
}

export default ReferalCode