package mwm.domain.usecases;

public interface UseCase<D, P> {
    P execute(D dto);
}