/** @type {import('next').NextConfig} */
const nextConfig = {
  async rewrites() {
    return [
      {
        source: "/api/:path*",
        destination: "https://sia-chatbot-backend-production.up.railway.app/api/:path*",
      },
    ];
  },
};

module.exports = nextConfig;
