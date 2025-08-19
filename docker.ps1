param (
    [Parameter(Mandatory=$false)]
    [ValidateSet("up","down", "restart", "logs", "build")]
    [string]$cmd = "up"
)

switch ($cmd) {
    "up" {
        Write-Host "Starting Fast API + Redis..." -ForegroundColor Green
        docker compose up --build
    }
    "down" {
        Write-Host "Stopping containers..." -ForegroundColor Yellow
        docker compose down
    }
    "restart" {
        Write-Host "Restarting containers..." -ForegroundColor Yellow
        docker compose restart
    }
    "logs" {
        Write-Host "Fetching logs..." -ForegroundColor Yellow
        docker compose logs -f
    }
    "build" {
        Write-Host "Building images..." -ForegroundColor Yellow
        docker compose build
    }
    default {
        Write-Host "Invalid command. Use 'up', 'down', 'restart', 'logs', or 'build'." -ForegroundColor Red
    }
}
