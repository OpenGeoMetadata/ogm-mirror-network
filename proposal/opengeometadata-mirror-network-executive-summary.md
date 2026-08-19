# OpenGeoMetadata API Mirror Network

## Shared infrastructure that becomes stronger with every new member

### Document control

| Field | Value |
| --- | --- |
| Status | **Draft for Community Discussion** |
| Document ID | `OGM-DISCUSSION-2026-01` |
| Version | `0.1.0` |
| Proposal lead | Eric Larson ([ewlarson@gmail.com](mailto:ewlarson@gmail.com)) |
| First published | August 19, 2026 |
| Last updated | August 19, 2026 |
| Sponsoring group | Seeking an OpenGeoMetadata community sponsor |
| Review period | Open; a closing date will be established by the sponsoring group |
| Discussion | [GitHub issue tracker](https://github.com/OpenGeoMetadata/ogm-mirror-network/issues); a dedicated review thread should be designated before formal review opens |
| Decision authority | To be designated by OGM governance before pilot authorization |
| Canonical source | [OpenGeoMetadata/ogm-mirror-network](https://github.com/OpenGeoMetadata/ogm-mirror-network) |
| Supersedes | None |
| Approval record | None; this document is not approved or normative |
| Document license | Proposed CC BY 4.0, subject to OGM community approval |

### Executive summary

**Companion document:** [Technical Implementation Guide](opengeometadata-api-mirror-network-technical-implementation.md)<br>
**Download:** [Two-page Executive Brief (PDF)](../output/pdf/opengeometadata-mirror-network-executive-brief.pdf)

OpenGeoMetadata has already solved the hardest community problems: a shared
discovery schema in OGM Aardvark, a distributed and transparent way to steward
metadata in GitHub, a proven API platform for harvesting and serving those
records, and the configurable OGM Discovery (`ogm-discovery`) frontend that can
be branded for an institution and hosted as a static site on GitHub Pages.

The next step is to make delivery as collaborative as the metadata.

The OpenGeoMetadata API Mirror Network would place a protected, health-aware global
endpoint in front of multiple institutional deployments of the OGM API. A
mirror-host institution would contribute one ordinary Linux virtual machine
and a technical contact. The OGM service operator would deploy and maintain the
containerized API stack with Kamal, keep the mirror synchronized with the public
OGM Aardvark repositories, monitor its readiness, and add it to the shared
traffic pool.

Every OGM Discovery site would use the same stable network API endpoint. Its theme
would present the adopting institution's brand and, when desired, scope search
results to that institution by default. The underlying API would still expose
the shared OGM corpus, enabling broader discovery and reuse.

This produces an unusually favorable exchange:

> An institution contributes the equivalent of one modest server and gains the
> foundation for a customizable, institution-branded geospatial discovery
> platform backed by the combined capacity and resilience of the
> OpenGeoMetadata community.

Crucially, capacity contribution and service adoption do not have to be
one-to-one. Institutions able to contribute a VM create shared headroom not
only for their own discovery sites, but also for smaller libraries that cannot
provide server infrastructure. A service-only adopter can publish Aardvark
metadata in GitHub, customize and brand OGM Discovery, and use the shared OGM API
endpoint without provisioning, securing, patching, or monitoring a local
backend. Its participation requires metadata stewardship and site
customization, not a campus application-hosting project.

That makes each contributed mirror a community multiplier. It expands service
capacity for current members, opens a nearly infrastructure-free path for new
members, and brings more institutions and collections into shared discovery.
The institutions with capacity lift the operating burden; the institutions
without capacity enrich the network's metadata, reach, and public value.

Growth no longer concentrates traffic and risk on one campus. Each new adopter
can strengthen the network through infrastructure, metadata, community reach,
or some combination of the three. Each new mirror makes the network harder to
overwhelm, less dependent on any single institution, and more useful to every
member. It also gives every mirror host a safe maintenance window: a local node
can be drained for operating-system or application upgrades while its discovery
site continues using the remaining network.

![OpenGeoMetadata API Mirror Network architecture](opengeometadata-mirror-network-architecture.svg)

## The proposal

Create a shared public read endpoint for OGM services, backed by a federation of
compatible API mirrors hosted by participating institutions.

1. **OpenGeoMetadata repositories remain the canonical source.** Institutions
   continue publishing public Aardvark records through the existing GitHub
   model. No institution gives up ownership or control of its metadata.
2. **Each mirror serves the full public corpus.** A mirror independently
   harvests and indexes the same OGM repositories using webhook events and
   scheduled reconciliation. The nodes do not need cross-campus database
   replication.
3. **A protected global edge manages public traffic.** A stable hostname applies
   caching where appropriate, rate limits and bot controls, checks each origin's
   health and data freshness, and routes requests by capacity and availability.
   A node can be taken out of rotation for planned maintenance without changing
   the public URL.
4. **OGM Discovery provides the institutional experience.** The static frontend
   runs on GitHub Pages, carries local branding and content in configuration,
   and queries the shared network endpoint. The frontend requires no local
   application server or mirror VM.
5. **Kamal makes operations repeatable.** The OGM operator deploys the same
   versioned container release to every mirror, stages upgrades, checks
   compatibility, and can roll back quickly.

The public edge should load balance only the read-oriented API surface. Admin,
harvest, deployment, and other privileged operations remain off the shared
public route. An origin is eligible for traffic only when its application
version, search services, record freshness, and capacity checks pass.

## Why directors should support it

### One contribution produces six returns

- **A public service without a local software project.** The institution gains a
  production-grade discovery backend and the foundation for a customizable,
  institution-branded frontend without assembling its own development team.
- **An inclusive path for institutions without infrastructure.** Mirror
  capacity is a pooled community contribution, not a condition of membership.
  A small library can adopt the shared backend, publish its metadata, and launch
  a branded discovery site without operating a VM or maintaining an API stack.
- **Protection against traffic spikes and abusive automation.** Edge controls
  absorb or reject unwanted traffic before it reaches campus systems, while
  healthy origins share legitimate requests.
- **Continuity through institutional outages.** Maintenance, network incidents,
  or a failed mirror do not require users to change URLs. Traffic moves to the
  remaining healthy nodes. Local teams gain time to patch, upgrade, test, and
  return their node to service without creating a public outage.
- **Shared improvements without repeated procurement.** New API capabilities,
  accessibility work, performance improvements, and frontend features can move
  through one common release path.
- **Visible participation in community infrastructure.** Mirror sponsors
  contribute durable capacity; service-only adopters contribute metadata,
  expertise, and reach. Both forms of participation benefit researchers and
  libraries across the network.

### The scaling model is the strategic advantage

A centralized service becomes more expensive and more fragile as adoption
grows. The mirror network reverses that relationship:

**new mirror host -> more shared capacity -> room for both mirror hosts and
service-only adopters -> broader discovery and stronger service -> easier next
adoption**

The result is cooperative infrastructure with horizontal capacity, geographic
diversity, and organizational redundancy. No single library has to provision
for the whole community's peak traffic, and no single campus becomes the
permanent point of failure.

## Two participation paths, one community service

Hardware is a valuable contribution, not an admission requirement.

| Participation path | Institution provides | Institution and community gain |
| --- | --- | --- |
| Mirror host | A production VM, campus network path, and technical contact | A branded discovery foundation, shared failover, maintenance freedom, and more capacity for the whole community |
| Service-only adopter | Public Aardvark metadata, frontend customization, and a service contact | A shared OGM API backend and branded discovery foundation with no local server or backend application operations |

An institution may begin as a service-only adopter and contribute a mirror
later, or host capacity before launching its own frontend. Governance should
recognize both as meaningful participation: one supplies shared infrastructure;
the other broadens the corpus, community, and impact that infrastructure serves.

### What a mirror host contributes and gains

| Participating institution provides | OGM service operator provides | Institution and community gain |
| --- | --- | --- |
| One production Linux VM | Kamal-based installation and upgrades | Foundation for a customizable, institution-branded OGM Discovery site |
| Public HTTPS connectivity from the network edge | API, database, search, cache, and worker configuration | Shared full-corpus OGM API |
| Firewall, DNS, SSH, and OS coordination | Metadata harvesting and indexing | Automatic failover and maintenance windows |
| A named technical and service contact | Health monitoring, traffic weights, rollback, and runbooks | Edge bot controls and rate limiting |
| Normal campus VM and network support | Compatibility testing and incident coordination | A voice in shared product governance |

The intended division is simple: **the institution hosts the machine; the OGM
network operates the application.**

## Cost and effort

### Reference mirror profile

The current BTAA production deployment is already a single-host Kamal design.
Its published production resource envelope reserves up to 8 CPUs and about 5 GB
for the web role, 1.75 CPUs and 2 GB for the worker, a 4 GB Elasticsearch heap,
and a Redis ceiling of 12 GB, in addition to PostgreSQL, Docker, filesystem
cache, and the operating system.

A conservative reference mirror therefore is:

| Resource | Planning specification |
| --- | --- |
| CPU | 16 vCPU, or 8 modern physical cores with simultaneous multithreading |
| Memory | 64 GB RAM; 32 GB is a pilot minimum subject to load testing |
| Storage | 500 GB usable SSD/NVMe, preferably protected by campus storage or disk redundancy |
| Network | 1 Gbps interface, stable public HTTPS path, normal outbound access to GitHub and the container registry |
| Operating system | Current Ubuntu LTS or equivalent, Docker, SSH key access |

This is deliberately ordinary infrastructure. As an August 2026 external price
benchmark, a Hetzner AX42-class dedicated server provides 8 physical cores / 16
threads, 64 GB RAM, two 512 GB NVMe drives, and a 1 Gbps connection for about
$117 per month before IPv4, tax, and setup. That is approximately **$1,405 per
year**. Limited inventory can be lower.

**A campus VM from existing capacity may have little or no incremental cost.**

**A service-only adopter has no OGM API server cost.** It uses capacity already
contributed to the network and needs no campus VM or local backend deployment.
Its effort is focused on metadata, OGM Discovery customization, and community
participation.

For budgeting, use **$1,500 per year per mirror node** as the target
infrastructure contribution, with local chargeback replacing the external
benchmark when applicable. This is not a procurement quote. A mainstream
public-cloud VM can cost materially more; the design does not require one.

The global edge, DNS, and shared monitoring are network-level costs rather than
per-institution costs. At pilot scale they should be budgeted centrally and are
expected to be small compared with even one local software implementation.

### Target mirror-host effort

- **One time:** 4-8 staff hours to provision the VM, establish DNS/firewall
  rules, confirm SSH access, and name contacts.
- **Ongoing:** at most a few host-support hours per quarter for OS maintenance,
  capacity changes, and campus networking. Application releases and routine
  data operations are handled centrally.
- **No local frontend server:** OGM Discovery builds and publishes through GitHub
  Pages.

For a service-only adopter, the VM, firewall, SSH, operating-system, and backend
support tasks disappear. The institution can participate without a local IT
deployment; only optional campus policies such as a custom domain may call for
local coordination.

These are pilot targets to validate, not contractual service levels.

## Alternatives considered

| Model | Principal advantage | Principal limitation |
| --- | --- | --- |
| One centrally hosted OGM API | Simplest initial operations and accountability | Concentrates cost, traffic, and service risk at one institution |
| Independent institution-specific stacks | Maximum local autonomy | Repeats deployment and operations work and preserves a high barrier for small institutions |
| CDN and web application firewall in front of one origin | Adds caching and bot protection | Leaves one origin as the capacity ceiling and operational failure domain |
| Federated OGM API mirror network **(recommended)** | Pools capacity, provides failover and maintenance freedom, and supports service-only adoption | Requires common releases, readiness standards, shared operations, and governance |

The recommended model is the only option considered that simultaneously grows
capacity with participation, preserves institutional hosting, and removes the
backend infrastructure requirement for smaller adopters.

## Open questions for community review

The draft deliberately leaves policy choices open where community authority is
required:

- Which OGM group will sponsor the proposal, and which body can authorize the
  pilot and any later production service?
- Who will fund and operate the global edge, DNS, shared monitoring, and incident
  coordination?
- What fair-use policy, capacity threshold, and onboarding criteria should apply
  to mirror hosts and service-only adopters?
- What service objectives, support boundaries, security expectations, and
  incident authority should the operating compact define?
- How should a mirror be retired, replaced, or temporarily removed from the
  network?
- Should the community adopt the proposed CC BY 4.0 document license?

## Draft review and decision process

Comments should be recorded in the repository's
[GitHub issue tracker](https://github.com/OpenGeoMetadata/ogm-mirror-network/issues).
Before a formal review period begins, the sponsoring group should designate one
issue or discussion as the canonical review thread, name the decision authority,
and publish a closing date. The proposal lead will publish numbered `0.x`
revisions and summarize material changes there. A pilot decision and its
rationale should be recorded publicly in this repository.

Proposed lifecycle:

**Community Discussion Draft -> Pilot Candidate -> Approved Pilot -> Production
Proposal -> Accepted, Rejected, Withdrawn, or Superseded**

### Revision history

| Version | Date | Editor | Summary |
| --- | --- | --- | --- |
| `0.1.0` | August 19, 2026 | Eric Larson | Initial formally controlled community discussion draft |

### Approval record

No approval has been recorded. Version `0.1.0` is a discussion document and does
not establish an OGM roadmap, service commitment, or technical standard.

## Operating safeguards

The network should launch with a short operating compact:

- **Version discipline:** mirrors run a supported, pinned OGM API release.
  Upgrades are staged, canaried, and reversible.
- **Maintenance without service interruption:** an institution can drain its
  mirror, complete OS or OGM API work on its own schedule, and rejoin only after
  readiness and freshness checks pass. Its public discovery site continues
  through other healthy mirrors.
- **Readiness, not simple uptime:** the edge checks API compatibility, search
  health, data freshness, and capacity before admitting a mirror to rotation.
- **Weighted participation:** traffic weights reflect each institution's stated
  capacity; a smaller node is still valuable and is not overloaded for the sake
  of even distribution.
- **Origin protection:** mirror addresses are not advertised as the primary
  public service. Firewalls should accept application traffic from the edge and
  restrict administrative access.
- **Rebuildable nodes:** GitHub Aardvark repositories remain canonical. Search
  indexes, caches, and public read databases are derived state that can be
  rebuilt, reducing backup complexity and vendor lock-in.
- **Transparent status:** members can see mirror health, software version,
  corpus freshness, and current traffic weight.
- **Clear responsibility:** OGM owns application operations and routing; mirror
  hosts own VM, OS, and campus network availability; service-only adopters have
  no backend host responsibility; the community owns schema and service policy.

## Recommended pilot

Authorize a 90-day, three-node pilot using the current BTAA node plus two
additional institutional mirror hosts. The pilot should also onboard at least
one service-only adopter that contributes no VM, proving that shared capacity
can remove the local backend IT requirement.

The pilot should prove six things:

1. A new institution can be provisioned with no local application development.
2. All mirrors serve a compatible API and sufficiently fresh corpus.
3. Loss of one node - or a planned node drain for an upgrade - causes no
   user-visible URL change and no manual intervention.
4. Bot controls and rate limits protect origins while legitimate traffic is
   distributed by health and capacity.
5. Aggregate tested capacity increases when a mirror joins the pool, while the
   measured institutional support burden remains within the target.
6. A service-only adopter can publish metadata and launch a customized discovery
   experience without provisioning or operating backend infrastructure.

At the end of the pilot, publish the measured onboarding time, operating effort,
cost, traffic distribution, failover result, and metadata freshness. Those
results become the evidence and onboarding package for the next institution.

## Decision requested

Approve the OpenGeoMetadata API Mirror Network as a shared-infrastructure pilot;
authorize a three-node implementation and a service-only adoption path;
designate appropriate service and technical contacts for each participation
mode; and charge the OGM working group with returning a production governance
and service-level proposal based on measured results.

The community has already created the schema, the metadata network, the API,
and the low-maintenance frontend. The mirror network is the piece that turns
those assets into durable, community-scale infrastructure.

## Foundations and planning sources

- [OpenGeoMetadata](https://opengeometadata.org/)
- [OpenGeoMetadata repositories on GitHub](https://github.com/opengeometadata)
- [BTAA Geospatial API](https://github.com/geobtaa/api)
- [OpenGeoMetadata API](https://github.com/ewlarson/ogm-api)
- [OGM Discovery (`ogm-discovery`)](https://github.com/ewlarson/ogm-discovery)
- [BTAA production Kamal configuration](https://github.com/geobtaa/api/blob/develop/config/deploy.prd.yml)
- [Hetzner AX42 hardware and June 2026 pricing](https://docs.hetzner.com/general/infrastructure-and-availability/price-adjustment/)
- [Cloudflare load balancing and health-aware routing](https://developers.cloudflare.com/load-balancing/)
