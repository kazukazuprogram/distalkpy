#!/usr/bin/env python3
# coding: utf-8

from voiceroid2api import VOICEROID2


def main():
    v = VOICEROID2()
    v.render("こんにちは", path="tset.wav")


if __name__ == '__main__':
    main()
