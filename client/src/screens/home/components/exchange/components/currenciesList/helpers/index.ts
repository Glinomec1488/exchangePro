const isSelectedCurrency = (
    isTo: boolean,
    currencyName: string,
    selectedFromCurrencyName: string,
    selectedToCurrencyName: string
) => {
    if (isTo) return currencyName === selectedToCurrencyName
    return currencyName === selectedFromCurrencyName
}

export const getActiveCurrencyStyle = (
    isTo: boolean,
    currencyName: string,
    selectedFromCurrencyName: string,
    selectedToCurrencyName: string
) => {
    return isSelectedCurrency(isTo, currencyName, selectedFromCurrencyName, selectedToCurrencyName) ? 'exchange__block-item_active' : ''
}