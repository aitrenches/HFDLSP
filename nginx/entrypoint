#!/usr/bin/bash
set -o errexit
set -o nounset

domains=(
        hfdlsp
)

function log {
        echo "$*" >&2
}

function warn {
        echo "WARNING: $*" >&2
}

for domain in "${domains[@]}"; do
        domainargs+=("--domain=$domain.trenches.ai")
done

log "Setting up certificates with certbot"
if certbot --non-interactive \
        --nginx \
        --expand \
        "${domainargs[@]}" \
        --reinstall \
        --agree-tos \
        --email=ops@trenches.ai \
        --redirect \
        --hsts
then
        log "Signaling nginx process run by certbot to terminate"
        kill "$(</var/run/nginx.pid)"

        log "Waiting for nginx process run by certbot to terminate"
        while [[ -e /var/run/nginx.pid ]]; do
                sleep 0.1
        done
else
        warn "Couldn't set up HTTPS"
fi

log "Starting nginx"
exec nginx -g "daemon off;"
