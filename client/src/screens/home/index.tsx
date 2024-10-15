import About from "./components/about"
import Exchange from "./components/exchange"
import HowExchange from "./components/howExchange"
import Support from "./components/support"
import TxHistory from "./components/txHistory"

const Home = () => {
    return (
        <main className="main">
            <About />
            <Exchange />
            <HowExchange />
            <TxHistory />
            <Support />
        </main>
    )
}

export default Home