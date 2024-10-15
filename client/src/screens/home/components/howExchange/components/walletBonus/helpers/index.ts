import { WalletBonusEnum } from "../enum"

export const chechWalletBonus = (address: string) => {
    const regex = /^(0x){1}[0-9a-fA-F]{40}$/i

    return regex.test(address)
}

export const getButtonStyles = (status: WalletBonusEnum) => {
    switch(status) { 
        case WalletBonusEnum.Default: return 'how-exchange__block-btn'
        case WalletBonusEnum.Confirmed: return 'how-exchange__block-btn how-exchange__block-btn-confirmed'
        case WalletBonusEnum.Denied: return 'how-exchange__block-btn how-exchange__block-btn-denied'
    }
}

export const getButtonText = (status: WalletBonusEnum, isPending: boolean) => {
    if (isPending) {
        return 'Checking your wallet...'
    }

    return status
}