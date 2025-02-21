// api/process.js
module.exports = async (req, res) => {
  const url = 'http://13.61.100.122/process';
  const fetch = await import('node-fetch').then(mod => mod.default);

  // Gérer CORS
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  try {
    // Transmission de la requête au serveur backend
    const response = await fetch(url, {
      method: req.method,
      headers: {
        'Content-Type': req.headers['content-type']
      },
      body: req.method !== 'GET' ? req.body : undefined
    });

    // Récupération du corps de la réponse
    const data = await response.buffer();

    // Transmission des en-têtes de réponse
    response.headers.forEach((value, key) => {
      res.setHeader(key, value);
    });

    // Envoi de la réponse
    res.status(response.status).send(data);
  } catch (error) {
    console.error('Proxy error:', error);
    res.status(500).json({ error: 'Une erreur est survenue lors de la connexion au serveur' });
  }
};
