import { useEffect, useState } from "react"
import { useAppDispatch, useAppSelector } from "../../../../../../../../store/hooks"
import { dispatchCaptchaResult, generateCaptcha } from "../../../../../../../../store/slices/exchange"

const Captcha = () => {
    const [result, setResult] = useState('')

    const {
        num1,
        num2,
        isValid,
    } = useAppSelector(state => state.exchange.captcha)

    const dispatch = useAppDispatch()

    useEffect(() => {
        if (!num1 && !num2) {
            dispatch(generateCaptcha())
        }
    }, [])

    return (
        <div className="exchange__block-wrapper">
            <div className="exchange__block-text">
                ENTER CAPTCHA
            </div>
            <div className="exchange__block-captcha">
                <input
                    className="exchange__block-input exchange__block-input-captcha exchange__block-input-captcha-first-num"
                    readOnly type="number" value={num1} />
                <div className="exchange__block-sign">+</div>
                <input
                    className="exchange__block-input exchange__block-input-captcha exchange__block-input-captcha-second-num"
                    readOnly type="number" value={num2} />
                <div className="exchange__block-sign">=</div>
                <input
                    className={
                        isValid
                            ? "exchange__block-input exchange__block-input-captcha exchange__block-input-captcha-sum"
                            : "exchange__block-input exchange__block-input-captcha exchange__block-input-captcha-sum exchange_wrong_captcha"
                    }
                    type="number" value={result} onChange={(e) => {
                        setResult(e.target.value)
                        dispatch(dispatchCaptchaResult(e.target.value))
                    }} name="captchaResult" required />
            </div>
        </div>
    )
}

export default Captcha