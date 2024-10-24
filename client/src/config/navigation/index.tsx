import {
  BrowserRouter as Router,
  Route,
  Routes,
  Navigate,
} from "react-router-dom";
import Chat from "../../components/chat";
import Footer from "../../components/footer";
import Header from "../../components/header";
import Home from "../../screens/home";
import Order from "../../screens/order";

const AppRouter = () => {
  return (
    <Router>
      <Header />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/order/:orderId" element={<Order />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
      <Footer />
      <Chat />
    </Router>
  );
};

export default AppRouter;
