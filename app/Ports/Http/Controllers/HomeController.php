<?php
declare(strict_types=1);

namespace App\Ports\Http\Controllers;

final class HomeController
{
    public function index(): void
    {
        header('Content-Type: text/html; charset=utf-8');
        echo "<h1>PRM Portafolio Academico</h1>";
        echo "<p>OK - Proyecto corriendo en XAMPP (macOS)</p>";
    }

    public function health(): void
    {
        header('Content-Type: application/json; charset=utf-8');
        echo json_encode(['status' => 'ok', 'app' => 'prm_portafolio']);
    }
}
