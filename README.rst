Description
===========

MTGA_Lister alows you to export your player stats, card collection and decks
from Magic The Gathering Arena to a text format suitable for use with
websites such as deckstats.net_ or software such as Cockatrice_.

.. _deckstats.net: http://deckstats.net/

.. _Cockatrice: https://cockatrice.github.io/

The program is for the moment Linux/wine only. There are lots of software
available for windows such as mtgatracker_ but Linux/wine needed something
too.

.. _mtgatracker: https://github.com/mtgatracker/mtgatracker

The project is at the moment a simple exporter, it doesn't provide any
overlay or tracking of win/loss ratios.

Documentation
=============

::

    Usage: mtga_lister [options] [DECK]

    Options:
        -h, --help              Print this help and exit
        -v, --version           Print version and exit
        -D, --database PATH     Path to the json database of card IDs
                                Default: ./mtga_db.json

    Arguments:
        DECK    ID of the deck to print. If missing prints the list of decks.

Dependencies
============

- python3
- docopt (https://github.com/docopt/docopt)

License
=======

This program is under the GPLv3 License.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
