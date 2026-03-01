<?php
declare(strict_types=1);

namespace App\Bootstrap;

use App\Ports\Http\Router\Router;
use App\Ports\Http\Controllers\HomeController;
use App\Ports\Http\Controllers\PortfolioController;
use App\Ports\Http\Controllers\CertificateController;

final class App
{
    private Container $container;
    private Router $router;

    public function __construct()
    {
        $this->container = new Container();
        $this->router = new Router();

        $this->router->get('/', [HomeController::class, 'index']);
        $this->router->get('/health', [HomeController::class, 'health']);

        $this->router->get('/portfolios', [PortfolioController::class, 'list']);
        $this->router->get('/portfolios/show', [PortfolioController::class, 'show']); // ?id=1
        $this->router->post('/portfolios/create', [PortfolioController::class, 'create']);

        $this->router->post('/certificates/generate', [CertificateController::class, 'generate']); // ?portfolio_id=1
    }

    public function run(): void
    {
        $method = $_SERVER['REQUEST_METHOD'] ?? 'GET';
        $path = parse_url($_SERVER['REQUEST_URI'] ?? '/', PHP_URL_PATH) ?: '/';

        $route = $this->router->match($method, $path);
        if (!$route) {
            http_response_code(404);
            echo "404 - Ruta no encontrada";
            return;
        }

        [$class, $action] = $route;
        $controller = $this->container->get($class);
        $controller->$action();
    }
}
