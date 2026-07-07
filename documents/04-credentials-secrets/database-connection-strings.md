> **SYNTHETIC TEST DATA.** All hostnames, credentials, and connection strings
> are fictional/inert and do not point at any real infrastructure. Generated
> for Netskope One DLP (credential/secret exfiltration) testing.

# config.prod.yaml — Example Leaked Application Configuration

Simulates an internal config/secrets file (the kind of thing that shouldn't
leave the corporate network, get pushed to a personal repo, or get pasted
into an external AI tool for "help fixing my connection error").

```yaml
environment: production

database:
  primary:
    engine: postgres
    host: prod-db-01.internal.lakesideoutfitters.corp
    port: 5432
    name: lakeside_core
    username: svc_app_prod
    password: Tr0ub4dor&3-Prod-2026!
    connection_string: "postgresql://svc_app_prod:Tr0ub4dor%263-Prod-2026%21@prod-db-01.internal.lakesideoutfitters.corp:5432/lakeside_core"

  replica:
    host: prod-db-02.internal.lakesideoutfitters.corp
    port: 5432
    username: svc_app_readonly
    password: R3adOnly!Pass2026

redis:
  host: prod-redis-01.internal.lakesideoutfitters.corp
  port: 6379
  password: R3d1sPassw0rd2026!

message_queue:
  provider: rabbitmq
  host: prod-mq-01.internal.lakesideoutfitters.corp
  username: mq_service
  password: MqS3rvic3Pass!2026

third_party:
  stripe_secret_key: sk_live_4eC39HqLyjWDarjtT1zdp7dcEXAMPLE00
  sendgrid_api_key: SG.EXAMPLE0000000000000000.EXAMPLE0000000000000000000000000000000000
  twilio_auth_token: 000000000000000000000000000000EX

encryption:
  data_at_rest_key_id: arn:aws:kms:us-east-2:000000000000:key/0000-0000-0000-0000-000000000000
  jwt_private_key_path: /etc/lakeside/secrets/throwaway_test_key.pem
```

See [`throwaway_test_key.pem`](./throwaway_test_key.pem) in this same folder —
a real, validly-formatted RSA private key generated **solely for this repo**
(via `openssl genpkey`), never used to protect anything, never registered with
any service, and safe to treat as fully synthetic. It exists so DLP engines
that look for a `-----BEGIN PRIVATE KEY-----` PEM block have a genuine one to
match against (rather than a truncated/fake-looking string that some
detectors might not recognize as PEM-shaped).

---
*Synthetic fixture — DLP testing only.*
