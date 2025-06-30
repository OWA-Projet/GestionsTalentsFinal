import { HttpInterceptorFn } from '@angular/common/http';

// Fonction pour décoder un JWT
function parseJwt(token: string): any {
  try {
    return JSON.parse(atob(token.split('.')[1]));
  } catch {
    return null;
  }
}

export const AuthInterceptor: HttpInterceptorFn = (req, next) => {
  const publicUrls = [
    "http://localhost:8000/api/offres-acceuil",
    // ... autres routes publiques
  ];

  // Si URL publique : on laisse passer sans token
  if (publicUrls.some(url => req.url.includes(url))) {
    return next(req);
  }

  let access: string | null = null;
  if (typeof window !== 'undefined') {
    access = localStorage.getItem('access');
  }

  if (access) {
    // Vérification d’expiration du token
    const decoded = parseJwt(access);
    if (decoded && decoded.exp) {
      const now = Date.now() / 1000; // secondes
      if (decoded.exp < now) {
        // Token expiré
        localStorage.clear();
        // Ici tu peux déclencher une redirection ou un toast/session expirée
        return next(req); // ou retourne une erreur personnalisée si tu veux bloquer
      }
    }
    // Token valide : injecte le header
    req = req.clone({
      setHeaders: { Authorization: `Bearer ${access}` }
    });
  }

  return next(req);
};
