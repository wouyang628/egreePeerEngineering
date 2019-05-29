# Egress Peer Engineering
Egree Peer Engineering with Healthbot and Northstar

Egress Peer Engineering enables the operator to direct traffic to a specific peer, set of peers, or a specific link to a peer based on business policy (cost) and performance information (latency, traffic loss, etc) other than the best path. The need for engineering the way that traffic exits the service provider AS is critical for ensuring cost efficiency while providing a good end user experience at the same time. 


Healthbot monitors peering links using OpenConfig, native Sensor, etc
When a peering link is in a bad state( delay, packet loss, etc),  Healthbot triggers API call to Northstar to steer the traffic by mapping the demands to a pre-configured colored SRTE LSP 
