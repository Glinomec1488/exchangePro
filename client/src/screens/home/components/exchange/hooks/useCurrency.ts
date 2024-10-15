import { useAppDispatch } from "../../../../../store/hooks"
import { dispatchFromCurrency, dispatchToCurrency } from "../../../../../store/slices/exchange"

const useCurrency = () => {
    const dispatch = useAppDispatch()

    const setFromCurrency = (shortName: string, fullName: string) => dispatch(dispatchFromCurrency({
        shortName,
        fullName
    }))
    const setToCurrency = (shortName: string, fullName: string) => dispatch(dispatchToCurrency({
        shortName,
        fullName
    }))

    return {
        setFromCurrency,
        setToCurrency,
    }
}

export default useCurrency