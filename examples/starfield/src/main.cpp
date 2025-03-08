#include "proteus.h"
#include "stars.h"

int main(int argc, char *argv[])
{
    initSDL(1920, 1080, "Raotating stars :)");
    stars_main(1920,1080);
    return 0;
}