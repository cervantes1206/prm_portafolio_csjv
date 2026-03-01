<?php
declare(strict_types=1);

namespace App\Ports\Http\Router;

final class Router
{
    private array $routes = ['GET' => [], 'POST' => []];

    public function get(string $path, array $handler): void { $this->routes['GET'][$path] = $handler; }
    public function post(string $path, array $handler): void { $this->routes['POST'][$path] = $handler; }

    public function match(string $method, string $path): ?array
    {
        $method = strtoupper($method);
        return $this->routes[$method][$path] ?? null;
    }
}
