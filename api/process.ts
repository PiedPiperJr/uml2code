import { VercelRequest, VercelResponse } from '@vercel/node';
import fetch from 'node-fetch';
import FormData from 'form-data';
import busboy from 'busboy';

export default async function handler(req: VercelRequest, res: VercelResponse) {
  // Gérer CORS
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  // Utiliser busboy pour parser le multipart/form-data
  const bb = busboy({ headers: req.headers });
  const formData = new FormData();

  let serverInputData: string | null = null;

  // Traiter les champs et fichiers
  bb.on('file', (name, file, info) => {
    const { filename, encoding, mimeType } = info;
    const chunks: Buffer[] = [];

    file.on('data', (data) => {
      chunks.push(data);
    });

    file.on('end', () => {
      const fileBuffer = Buffer.concat(chunks);
      formData.append(name, fileBuffer, { filename });
    });
  });

  bb.on('field', (name, val) => {
    if (name === 'data') {
      serverInputData = val;
    }
    formData.append(name, val);
  });

  // Quand tout est traité, envoyer au serveur backend
  bb.on('close', async () => {
    try {
      console.log('Forwarding request to backend...');

      const response = await fetch('http://13.61.100.122:5000/process', {
        method: 'POST',
        body: formData,
        headers: formData.getHeaders()
      });

      if (!response.ok) {
        console.error('Backend returned error:', response.status);
        return res.status(response.status).json({
          error: `Backend returned ${response.status}`
        });
      }

      const contentType = response.headers.get('content-type');
      const buffer = await response.buffer();

      // Transférer les en-têtes importants
      if (contentType) {
        res.setHeader('Content-Type', contentType);
      }
      if (response.headers.has('content-disposition')) {
        const disposition = response.headers.get('content-disposition');
        if (disposition) {
          res.setHeader('Content-Disposition', disposition);
        }
      }

      // Envoyer la réponse
      res.status(response.status).send(buffer);

    } catch (error) {
      console.error('Proxy error:', error);
      res.status(500).json({ error: 'Internal server error' });
    }
  });

  // Passer la requête à busboy
  req.pipe(bb);
}
