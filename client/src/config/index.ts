import { getEnv } from "../utils";

export const serveUrl = getEnv(process.env.REACT_APP_SERVER_URL, 'REACT_APP_SERVER_URL')