class MinimaxBot {
 public:
  GameAction getNextAction(const Game &game, int pId) {
    int teamId = pId;
    int oTeamId = 1 - pId;

    for (int sId : game.players[teamId].shipsAlive) {
      const Ship &ship = game.ships[sId];

      // Find the closest opponent ship
      int closestosId = -1;
      int minD = INT_MAX;
      for (int osId : game.players[oTeamId].shipsAlive) {
        const Ship &oppShip = game.ships[osId];
        int d = ship.offBow.distSafe(oppShip.offBow);
        if (d < minD) {
          minD = d;
          closestosId = osId;
        }
      }

      vector<BoatAction> myActions{BoatAction(AType::Faster), BoatAction(AType::Slower), BoatAction(AType::Port),
                                   BoatAction(AType::Star),   BoatAction(AType::Mine),   BoatAction(AType::Wait)};
      vector<BoatAction> oppActions(myActions);
    }
    return GameAction();
  }
};
MetaBot _minimaxBot;