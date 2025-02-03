package org.enspy.4gi.domain.usecases;

public interface UseCase<D, P> {
    P execute(D dto);
}