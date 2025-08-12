import { NextApiRequest, NextApiResponse } from 'next';
import httpProxy from 'http-proxy';

const proxy = httpProxy.createProxyServer();

export const config = {
  api: {
    bodyParser: false,
  },
};

export default (req: NextApiRequest, res: NextApiResponse) => {
  req.headers['X-API-Key'] = process.env.API_KEY;
  proxy.web(req, res, {
    target: 'http://localhost:8000',
    changeOrigin: true,
  });
};