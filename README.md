# Privy Router

> Privy Router is responsible for taking commands from clients (Privy CLI or Privy Messenger) and deleagating them to an appropriate Privy Daemon. It is also responsible for the lifetime management of said daemons.

As of right now, in order to run privy daemons, Docker and the privyd docker images need to be installed. This is required since privy daemons are dynamically started  and stopped as separate processes during the runtime of the Privy Router. Unfortunately the js-ipfs module (which the daemons use internally) doesn't support setting the ipfs node's ports (rather it defaults to a given value), hence the need for containerizing the nodes, then port mapping the containers apropriately.

