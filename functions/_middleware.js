// Bloqueia programas de cópia de sites (HTTrack, wget, scrapers) na página.
// Roda só no HTML (ver public/_routes.json) para não gastar execuções com as fotos.
// Robôs do Google (Googlebot, AdsBot), do WhatsApp e das redes sociais continuam liberados.

const COPIADORES = /httrack|webcopier|webzip|teleport|offline explorer|sitesucker|website downloader|webreaper|wget|curl\/|python-requests|python-urllib|aiohttp|httpx|scrapy|go-http-client|java\/|libwww|node-fetch|axios|headlesschrome|phantomjs|puppeteer|playwright|site-shot|webcopy|getright|pavuk|grabber|extractor|ahrefs|semrush|mj12bot|dotbot|petalbot|bytespider|ccbot|gptbot|claudebot/i;
const LIBERADOS = /googlebot|adsbot-google|google-inspectiontool|mediapartners-google|apis-google|google-read-aloud|feedfetcher-google|bingbot|whatsapp|facebookexternalhit|facebot|meta-externalagent|instagram|twitterbot|linkedinbot|telegrambot|slackbot|discordbot/i;

export async function onRequest({ request, next }) {
  const ua = request.headers.get('user-agent') || '';

  if (!LIBERADOS.test(ua) && (COPIADORES.test(ua) || ua.trim() === '')) {
    return new Response('Acesso não permitido.', { status: 403, headers: { 'content-type': 'text/plain; charset=utf-8' } });
  }

  return next();
}
