import { configureStore } from '@reduxjs/toolkit'
import exchange from './slices/exchange'

export const store = configureStore({
    reducer: {
        exchange: exchange
    },
})

export type RootState = ReturnType<typeof store.getState>
export type AppDispatch = typeof store.dispatch