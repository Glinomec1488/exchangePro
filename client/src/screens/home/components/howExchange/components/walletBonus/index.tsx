import { wait } from "@testing-library/user-event/dist/utils"
import { useEffect, useState } from "react"
import { WalletBonusEnum } from "./enum"
import { chechWalletBonus, getButtonStyles, getButtonText } from "./helpers"

const WalletBonus = () => {
    const [address, setAddress] = useState('')
    const [isPending, setIsPending] = useState(false)
    const [buttonStatus, setButtonStatus] = useState(WalletBonusEnum.Default)

    const handleRequest = async () => {
        setIsPending(true)

        const isValidAddress = chechWalletBonus(address)

        await wait(1500)

        if (!isValidAddress) {
            setButtonStatus(WalletBonusEnum.Denied)
        } else {
            setButtonStatus(WalletBonusEnum.Confirmed)
        }
        
        setIsPending(false)
        await wait(1500)
        setButtonStatus(WalletBonusEnum.Default)
    }

    return (
        <div className="how-exchange__block">
            <div className="how-exchange__block-step">
                Step #1
            </div>
            <h4 className="how-exchange__block-title">
                Check your wallet for 15% bonus!
            </h4>
            <div className="how-exchange__block-text">
                Enter your address to receive bonus!
            </div>
            <input
                className="how-exchange__block-input"
                type="text"
                placeholder="Any coin address"
                value={address}
                onChange={e => setAddress(e.target.value)}
            />
            <button onClick={() => handleRequest()} className={getButtonStyles(buttonStatus)}>
                {
                    getButtonText(buttonStatus, isPending)
                }
            </button>
        </div>
    )
}

export default WalletBonus